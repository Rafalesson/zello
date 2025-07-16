// src/components/ui/Input.tsx
import React from 'react';
import { twMerge } from 'tailwind-merge';
import { clsx } from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon?: React.ReactNode; // Propriedade opcional para o ícone
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, id, type = 'text', icon, ...props }, ref) => {
    return (
      <div className="w-full">
        <label htmlFor={id} className="block text-sm font-medium text-slate-700 mb-2">
          {label}
        </label>
        <div className="relative">
          {/* Se um ícone for fornecido, ele é posicionado aqui */}
          {icon && (
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              {React.cloneElement(icon as React.ReactElement, {
                className: "h-5 w-5 text-slate-400",
              })}
            </div>
          )}
          <input
            id={id}
            ref={ref}
            type={type}
            className={twMerge(clsx(
              "block w-full rounded-lg border border-slate-300 bg-white px-4 py-2 text-slate-900 shadow-sm placeholder:text-slate-400 transition-colors duration-300 focus:border-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900/50 sm:text-sm",
              // Adiciona padding à esquerda se houver um ícone
              icon ? "pl-10" : "px-4",
              className
            ))}
            {...props}
          />
        </div>
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };