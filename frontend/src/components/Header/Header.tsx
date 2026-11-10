import { NavLink } from "react-router-dom";
import "./styles.css"

const links = [
  { to: "/upload", label: "Импорт структурированных данных" },
  { to: "/raw_data", label: "Исходные данные" },
  { to: "/clean_data", label: "Очищенные данные" },
  { to: "/raw_weather", label: "Сырые данные" },
  { to: "/weather", label: "Извлечённые данные" },
  { to: "/features", label: "Итоговые данные" },
  { to: "/baseline", label: "Базовая модель" },
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