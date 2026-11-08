import { NavLink } from "react-router-dom";
import "./styles.css"

const links = [
  { to: "/upload", label: "Импорт данных" },
  { to: "/data", label: "Данные" },
  { to: "/dash", label: "Дашборд" },
];

export const Header = () => {
  return (
    <header className="header">
      <nav className="header-nav">
        {links.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `header-link${isActive ? " header-link--active" : ""}`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
};