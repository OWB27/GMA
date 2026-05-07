import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "../../lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-[32px] border text-xs font-bold uppercase tracking-[1.17px] transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-40",
  {
    variants: {
      variant: {
        ghost:
          "border-[rgba(240,240,250,0.42)] bg-[rgba(240,240,250,0.1)] text-[#f0f0fa] hover:bg-[rgba(240,240,250,0.2)]",
        quiet:
          "border-[rgba(240,240,250,0.24)] bg-transparent text-[#f0f0fa] hover:bg-[rgba(240,240,250,0.1)]",
      },
      size: {
        default: "h-12 px-[18px]",
        sm: "h-10 px-4",
      },
    },
    defaultVariants: {
      variant: "ghost",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button ref={ref} className={cn(buttonVariants({ variant, size, className }))} {...props} />
  ),
);
Button.displayName = "Button";

export { Button };
