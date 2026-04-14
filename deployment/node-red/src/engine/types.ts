import type { Node, NodeDef } from 'node-red';

export interface DeployConfig extends NodeDef {
    kubeconfigContent: string;
    privateKeyContent: string;
    certificateContent: string;
    domainAddress: string;
    instanceName: string;
    oidcIssuerUrl: string;
    clientId: string;
}

export interface DeployNode extends Node {
    ingressExternalIp?: string;
    dcsUrl?: string;
}
