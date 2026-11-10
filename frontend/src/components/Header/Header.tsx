import { NavLink } from "react-router-dom";
import "./styles.css"

const links = [
  { to: "/upload", label: "Импорт структурированных данных" },
  { to: "/data_raw", label: "Структурированные данные (СД)" },
  { to: "/data_clean", label: "Очищенные СД" },
  { to: "/weather_raw", label: "Неструктурированные данные (НД)" },
  { to: "/weather_parsed", label: "Извлеченные НД" },
  { to: "/weather_clean", label: "Очищенные НД" },
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