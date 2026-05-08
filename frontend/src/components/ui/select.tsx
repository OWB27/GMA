import * as React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";

import { cn } from "../../lib/utils";

const Select = SelectPrimitive.Root;
const SelectValue = SelectPrimitive.Value;
const SelectPrimitiveTrigger = SelectPrimitive.Trigger as unknown as React.ComponentType<Record<string, unknown>>;
const SelectPrimitiveIcon = SelectPrimitive.Icon as unknown as React.ComponentType<Record<string, unknown>>;
const SelectPrimitiveContent = SelectPrimitive.Content as unknown as React.ComponentType<Record<string, unknown>>;
const SelectPrimitiveViewport = SelectPrimitive.Viewport as unknown as React.ComponentType<Record<string, unknown>>;
const SelectPrimitiveItem = SelectPrimitive.Item as unknown as React.ComponentType<Record<string, unknown>>;
const SelectPrimitiveItemText = SelectPrimitive.ItemText as unknown as React.ComponentType<Record<string, unknown>>;

type SelectTriggerProps = React.ComponentPropsWithoutRef<"button"> & {
  children?: React.ReactNode;
};

const SelectTrigger = React.forwardRef<HTMLButtonElement, SelectTriggerProps>(
  ({ className, children, ...props }, ref) => (
  <SelectPrimitiveTrigger
    ref={ref as never}
    className={cn(
      "flex h-12 w-full items-center justify-between border-b border-[rgba(240,240,250,0.42)] bg-black/40 px-0 py-2 text-left font-din text-base uppercase tracking-[0.96px] text-[#f0f0fa] outline-none transition-colors focus:border-[#f0f0fa] disabled:cursor-not-allowed disabled:opacity-40",
      className,
    )}
    {...props}
  >
    {children}
    <SelectPrimitiveIcon className="ml-4 text-[rgba(240,240,250,0.72)]">⌄</SelectPrimitiveIcon>
  </SelectPrimitiveTrigger>
  ),
);
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;

type SelectContentProps = React.ComponentPropsWithoutRef<"div"> & {
  children?: React.ReactNode;
  position?: "item-aligned" | "popper";
};

const SelectContent = React.forwardRef<HTMLDivElement, SelectContentProps>(
  ({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitiveContent
      ref={ref as never}
      position={position}
      sideOffset={8}
      className={cn(
        "z-50 max-h-80 min-w-[var(--radix-select-trigger-width)] overflow-hidden rounded-[18px] border border-[rgba(240,240,250,0.28)] bg-black/95 font-din text-[#f0f0fa] shadow-none backdrop-blur-md",
        className,
      )}
      {...props}
    >
      <SelectPrimitiveViewport className="p-2">{children}</SelectPrimitiveViewport>
    </SelectPrimitiveContent>
  </SelectPrimitive.Portal>
  ),
);
SelectContent.displayName = SelectPrimitive.Content.displayName;

type SelectItemProps = React.ComponentPropsWithoutRef<"div"> & {
  children?: React.ReactNode;
  value: string;
};

const SelectItem = React.forwardRef<HTMLDivElement, SelectItemProps>(
  ({ className, children, ...props }, ref) => (
  <SelectPrimitiveItem
    ref={ref as never}
    className={cn(
      "relative flex h-10 cursor-default select-none items-center rounded-[12px] px-3 font-din text-sm uppercase tracking-[0.96px] outline-none data-[highlighted]:bg-[rgba(240,240,250,0.14)] data-[highlighted]:text-[#f0f0fa] data-[state=checked]:bg-[rgba(240,240,250,0.1)]",
      className,
    )}
    {...props}
  >
    <SelectPrimitiveItemText>{children}</SelectPrimitiveItemText>
  </SelectPrimitiveItem>
  ),
);
SelectItem.displayName = SelectPrimitive.Item.displayName;

export { Select, SelectContent, SelectItem, SelectTrigger, SelectValue };
