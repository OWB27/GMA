import * as React from "react";

import { cn } from "../../lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        "h-12 w-full border-b border-[rgba(240,240,250,0.42)] bg-transparent px-0 py-2 text-base uppercase tracking-[0.96px] text-[#f0f0fa] outline-none placeholder:text-[rgba(240,240,250,0.48)] focus:border-[#f0f0fa]",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";

export { Input };
