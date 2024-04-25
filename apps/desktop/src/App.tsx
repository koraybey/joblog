import { ThemeProvider } from '@/components/theme-provider'

import { useVacancy } from './hooks/useVacancy'
import { columns } from './jobs/columns'
import { DataTable } from './jobs/data-table'

const App = () => {
    const { data, isLoading } = useVacancy()
    if (!data || isLoading) return
    return (
        <ThemeProvider defaultTheme={'dark'} storageKey={'vite-ui-theme'}>
            <DataTable columns={columns} data={data?.allVacancies} />
        </ThemeProvider>
    )
}

export default App
