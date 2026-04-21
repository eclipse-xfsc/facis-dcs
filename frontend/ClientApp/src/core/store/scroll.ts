import { defineStore } from 'pinia'
import { useTemplateRef } from 'vue'

export const useScrollStore = defineStore('scroll', () => {
  const scrollContainer = useTemplateRef<HTMLElement>('scrollContainer')

  function scrollToTop() {
    scrollContainer.value?.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }

  return { scrollContainer, scrollToTop }
})
