import { useCallback, useEffect, useState } from "react";
import type { Page } from "../types.ts";

type UseListOptions = {
  url: string;
  pageSize?: number;
};

export const useList = <T,>({ url, pageSize }: UseListOptions) => {
  const [page, setPage] = useState(1);
  const [data, setData] = useState<Page<T>>({ items: [], total: 0 });
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page: String(page) });

      const res = await fetch(`${url}?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      setData(await res.json());
    } catch (e) {
      alert(e instanceof Error && e.message.startsWith("HTTP")
        ? "Ошибка при загрузке"
        : "Нет связи с сервером");
    } finally {
      setLoading(false);
    }
  }, [url, page, pageSize]);

  useEffect(() => {
    load();
  }, [load]);

  return { ...data, page, setPage, loading, reload: load };
};