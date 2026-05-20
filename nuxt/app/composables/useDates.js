import dayjs from 'dayjs'
import 'dayjs/locale/es'
import localizedFormat from 'dayjs/plugin/localizedFormat'

dayjs.extend(localizedFormat)
dayjs.locale('es')

export function useDates() {
  const months_of_year = [
    { name: 'Enero', short_name: 'Ene' },
    { name: 'Febrero', short_name: 'Feb' },
    { name: 'Marzo', short_name: 'Mar' },
    { name: 'Abril', short_name: 'Abr' },
    { name: 'Mayo', short_name: 'May' },
    { name: 'Junio', short_name: 'Jun' },
    { name: 'Julio', short_name: 'Jul' },
    { name: 'Agosto', short_name: 'Ago' },
    { name: 'Septiembre', short_name: 'Sep' },
    { name: 'Octubre', short_name: 'Oct' },
    { name: 'Noviembre', short_name: 'Nov' },
    { name: 'Diciembre', short_name: 'Dic' },
  ]

  // 'L' usa el formato corto localizado: con locale 'es' → DD/MM/YYYY
  function formatDate(dateStr) {
    if (!dateStr) return '—'
    return dayjs(dateStr).format('L')
  }

  return {
    months_of_year,
    formatDate,
  }
}