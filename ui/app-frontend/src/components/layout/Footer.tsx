// src/components/layout/Footer.tsx
export function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-white">
      <div className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-slate-500">
          &copy; {currentYear} Zello. Todos os direitos reservados.
        </p>
      </div>
    </footer>
  );
}