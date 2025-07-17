// src/components/ui/Carousel.tsx
"use client"

import * as React from "react"
import useEmblaCarousel, { type EmblaOptionsType } from "embla-carousel-react"
import Autoplay from "embla-carousel-autoplay"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "./Button"
import { twMerge } from "tailwind-merge"
import { clsx } from "clsx"

type CarouselProps = {
  options?: EmblaOptionsType
}

export function Carousel({ children, options }: React.PropsWithChildren<CarouselProps>) {
  // Configura o carrossel com autoplay de 7 segundos
  const [emblaRef, emblaApi] = useEmblaCarousel(
    {
      loop: true,
      align: "start",
      ...options,
    },
    [Autoplay({ delay: 7000, stopOnInteraction: false, stopOnMouseEnter: true })]
  );

  // Funções para os botões de navegação
  const scrollPrev = React.useCallback(() => emblaApi?.scrollPrev(), [emblaApi]);
  const scrollNext = React.useCallback(() => emblaApi?.scrollNext(), [emblaApi]);

  return (
    <div className="relative group" aria-roledescription="carousel">
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex touch-pan-y">{children}</div>
      </div>

      <Button
        variant="outline"
        size="icon"
        className="absolute left-4 md:left-8 top-1/2 -translate-y-1/2 h-10 w-10 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 bg-white/50 hover:bg-white"
        onClick={scrollPrev}
        aria-label="Slide anterior"
      >
        <ChevronLeft className="h-6 w-6" />
      </Button>

      <Button 
        variant="outline" 
        size="icon" 
        className="absolute right-4 top-1/2 -translate-y-1/2 h-10 w-10 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 bg-white/50 hover:bg-white"
        onClick={scrollNext}
        aria-label="Próximo slide"
      >
        <ChevronRight className="h-6 w-6" />
      </Button>
    </div>
  )
}

export function CarouselItem({ children, className }: React.PropsWithChildren<{className?: string}>) {
  return (
    <div className={twMerge(clsx("min-w-0 flex-shrink-0 flex-grow-0 basis-full pl-4", className))} aria-roledescription="slide">
        {children}
    </div>
  )
}