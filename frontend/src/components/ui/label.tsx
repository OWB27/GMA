import * as React from "react";

import { cn } from "../../lib/utils";

const Label = React.forwardRef<HTMLLabelElement, React.LabelHTMLAttributes<HTMLLabelElement>>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={cn("text-[0.63rem] font-bold uppercase leading-none tracking-[1px] text-[#f0f0fa]", className)}
      {...props}
    />
  ),
);
Label.displayName = "Label";

export { Label };
