/**
 * Server-side (Node.js / Node-RED runtime).
 * Handles the deploy operation: writes credential temp files, invokes deploy.sh,
 * parses its output, and updates the node's status and properties.
 */
import { exec } from 'child_process';
import * as fs from 'fs';
import * as tmp from 'tmp';
import * as path from 'path';
import type { NodeMessage } from 'node-red';

import { SCRIPTS_DIR } from './paths';
import type { DeployConfig, DeployNode } from './types';

type TmpFile = ReturnType<typeof tmp.fileSync>;

function writeTempFiles(config: DeployConfig): { kubeTmp: TmpFile; keyTmp: TmpFile; crtTmp: TmpFile } {
    const kubeTmp = tmp.fileSync({ prefix: 'kube-', postfix: '.yaml' });
    fs.writeFileSync(kubeTmp.name, config.kubeconfigContent);
    const keyTmp = tmp.fileSync({ prefix: 'key-', postfix: '.key' });
    fs.writeFileSync(keyTmp.name, config.privateKeyContent);
    const crtTmp = tmp.fileSync({ prefix: 'crt-', postfix: '.crt' });
    fs.writeFileSync(crtTmp.name, config.certificateContent);
    return { kubeTmp, keyTmp, crtTmp };
}

function parseDeployOutput(stdout: string): Record<string, string> {
    const res: Record<string, string> = {};
    stdout.split(/\r?\n/).forEach(line => {
        let m: RegExpMatchArray | null;
        if      ((m = line.match(/^🔹 ingress External-IP: (.+)$/))) res.ingressExternalIp = m[1];
        else if ((m = line.match(/^🔹 DCS URL:\s+(.+)$/)))           res.dcsUrl = m[1];
    });
    return res;
}

/**
 * Runs deploy.sh with the node's configuration.
 * Called from the node's 'input' event handler.
 *
 * deploy.sh <kubeconfig> <key> <cert> <domain> <path> <oidc_issuer_url> <oidc_client_id>
 */
export function deploy(node: DeployNode, config: DeployConfig, msg: NodeMessage): void {
    let kubeTmp: TmpFile, keyTmp: TmpFile, crtTmp: TmpFile;
    try {
        ({ kubeTmp, keyTmp, crtTmp } = writeTempFiles(config));
    } catch (err: unknown) {
        node.error(`Failed to write temp files: ${(err as Error).message}`, msg);
        node.status({ fill: 'red', shape: 'ring', text: 'file error' });
        return;
    }

    const clientId = config.clientId || 'digital-contracting-service';
    const args = [
        kubeTmp.name,
        keyTmp.name,
        crtTmp.name,
        config.domainAddress,
        config.instanceName,
        config.oidcIssuerUrl,
        clientId,
    ];
    const cmd = `bash ${JSON.stringify(path.join(SCRIPTS_DIR, 'deploy.sh'))} ` + args.map(a => JSON.stringify(a)).join(' ');

    node.log(`Executing: ${cmd}`);
    node.status({ fill: 'blue', shape: 'dot', text: 'deploying' });

    exec(cmd, { cwd: SCRIPTS_DIR }, (err, stdout, stderr) => {
        try { kubeTmp.removeCallback(); keyTmp.removeCallback(); crtTmp.removeCallback(); } catch (_) { /* ignore */ }

        if (err) {
            const errorMsg = stderr || err.message;
            node.error(errorMsg, msg);
            node.status({ fill: 'red', shape: 'ring', text: 'deploy failed' });
            msg.payload = errorMsg;
            node.send(msg);
            return;
        }

        const res = parseDeployOutput(stdout);
        node.ingressExternalIp = res.ingressExternalIp;
        node.dcsUrl = res.dcsUrl;

        node.log(`Deployment result: ${JSON.stringify(res)}`);
        node.status({ fill: 'green', shape: 'dot', text: 'deployed' });

        msg.payload = res;
        node.send(msg);
    });
}
