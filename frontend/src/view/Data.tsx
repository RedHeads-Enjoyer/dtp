import { useState, useEffect } from "react";
import type { DtpPage } from "../types.ts";
import {formatDate} from "../utils.ts";

export const Data = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [pageNum, setPageNum] = useState<number>(1);
  const [data, setData] = useState<DtpPage>({
    items: [],
    total: 0,
    page: 1,
    pages: 0,
  });

  const loadData = async (page: number): Promise<void> => {
    setLoading(true);

    try {
      const res = await fetch(`/api/dtp?page=${page}`);

      if (!res.ok) {
        alert("Ошибка при загрузке");
        return;
      }

      const result: DtpPage = await res.json();
      setData(result);
    } catch {
      alert("Нет связи с сервером");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(pageNum);
  }, [pageNum]);

  const { items, total, page, pages } = data;

  return (
    <div className="list-wrapper">
      <div className="list-meta-header">
        <div className="list-total">
          Всего записей: {total.toLocaleString("ru-RU")}
        </div>

        <div className="list-pager">
          <button
            onClick={() => setPageNum(page - 1)}
            disabled={loading || page <= 1}
          >
            Назад
          </button>

          <span className="list-pager-info">
            Страница {page} из {pages}
          </span>

          <button
            onClick={() => setPageNum(page + 1)}
            disabled={loading || page >= pages}
          >
            Вперёд
          </button>
        </div>
      </div>

      {loading && <div className="list-status">Загрузка данных...</div>}

      <div className="list-table-wrap">
        <table className="list-table">
          <thead>
            <tr>
              <th>Дата</th>
              <th>Регион</th>
              <th>Адрес</th>
              <th>Категория</th>
              <th>Тяжесть</th>
              <th>Погода</th>
              <th className="num">Участников</th>
              <th className="num">Погибло</th>
              <th className="num">Ранено</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{formatDate(item.datetime)}</td>
                <td>{item.region}</td>
                <td className="list-address" title={item.address}>
                  {item.address}
                </td>
                <td>{item.category}</td>
                <td>{item.severity}</td>
                <td>{item.weather}</td>
                <td className="num">{item.participants_count}</td>
                <td className="num">{item.dead_count}</td>
                <td className="num">{item.injured_count}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {items.length === 0 && !loading && (
          <div className="list-empty">Нет данных</div>
        )}
      </div>
    </div>
  );
};