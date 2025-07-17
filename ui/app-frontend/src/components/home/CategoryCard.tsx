// src/components/home/CategoryCard.tsx
import Link from "next/link";
import React from "react";

interface CategoryCardProps {
  icon: React.ReactNode;
  title: string;
  items: string[];
}

export function CategoryCard({ icon, title, items }: CategoryCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 transition-shadow hover:shadow-md">
      <div className="flex items-center gap-4 mb-4">
        <div className="text-slate-700">{icon}</div>
        <h3 className="font-bold text-lg text-slate-800">{title}</h3>
      </div>
      <ul className="space-y-3">
        {items.map((item) => (
          <li key={item}>
            <Link
              href="#"
              className="text-slate-600 hover:text-slate-900 hover:underline transition-colors"
            >
              {item}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}