// src/components/ui/Card.tsx
import * as React from "react"
import { twMerge } from "tailwind-merge"
import { clsx } from "clsx"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={twMerge(
      "rounded-xl border bg-white text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={twMerge("p-6", className)} {...props} />
))
CardContent.displayName = "CardContent"

export { Card, CardContent };