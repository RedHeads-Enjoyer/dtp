import { useCallback, useEffect, useState } from "react";
import type {DashboardData} from "../types.ts";

export const useDashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/dashboard");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (e) {
      alert(
        e instanceof Error && e.message.startsWith("HTTP")
          ? "Ошибка при загрузке дашборда"
          : "Нет связи с сервером"
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { data, loading, reload: load };
};
