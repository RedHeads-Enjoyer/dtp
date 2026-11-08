import { Loader } from "../Loader/Loader.tsx";
import "./styles.css";
import type { ReactNode } from "react";
import {Button} from "../Button/Button.tsx";

type Align = "left" | "center" | "right";

export type Column<T> = {
  key: string;
  header: string;
  render: (item: T) => ReactNode;
  align?: Align;
  className?: string;
};

type Pager = {
  page: number;
  pages: number;
  onChange: (page: number) => void;
};

type ListProps<T extends { id: number | string }> = {
  items: T[];
  total: number;
  columns: Column<T>[];
  loading: boolean;
  emptyText?: string;
  pager?: Pager;
  header?: ReactNode;
};

const ALIGN_CLASS: Record<Align, string | undefined> = {
  left: undefined,
  center: "cell-center",
  right: "num",
};

const cellClass = <T,>(c: Column<T>) =>
  [ALIGN_CLASS[c.align ?? "left"], c.className].filter(Boolean).join(" ") || undefined;

export const List = <T extends { id: number | string }>({
  items,
  total,
  columns,
  loading,
  emptyText = "Нет данных",
  pager,
  header,
}: ListProps<T>) => {
  return (
    <div className="list-wrapper">
      <div className="list-meta-header">
        <div className="list-total">
          Всего записей: {total.toLocaleString("ru-RU")}
        </div>

        {pager && pager.pages > 1 && (
          <div className="list-pager">
            <Button
              onClick={() => pager.onChange(pager.page - 1)}
              disabled={loading || pager.page <= 1}
            >
              Назад
            </Button>
            <span className="list-pager-info">
              Страница {pager.page} из {pager.pages}
            </span>
            <Button
              onClick={() => pager.onChange(pager.page + 1)}
              disabled={loading || pager.page >= pager.pages}
            >
              Вперёд
            </Button>
          </div>
        )}
      </div>

      {header}

      <div className="list-table-wrap">
        <table className="list-table">
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={c.key} className={cellClass(c)}>
                  {c.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
          {loading ?
            <div className="list-status">
              <Loader size={16} label="Загрузка данных..." />
            </div>
            : items.map((item) => (
              <tr key={item.id}>
                {columns.map((c) => (
                  <td key={c.key} className={cellClass(c)}>
                    {c.render(item)}
                  </td>
                ))}
              </tr>
            ))
          }
          </tbody>
        </table>

        {items.length === 0 && !loading && (
          <div className="list-empty">{emptyText}</div>
        )}
      </div>
    </div>
  );
};