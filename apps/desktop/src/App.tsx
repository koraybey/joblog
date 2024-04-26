import { Building2 } from 'lucide-react'
import * as R from 'ramda'
import { useEffect } from 'react'
import Markdown from 'react-markdown'
import { create } from 'zustand'
import { createJSONStorage, devtools, persist } from 'zustand/middleware'

import { ThemeProvider } from '@/components/theme-provider'

import { Vacancy } from './__generated__/gql/graphql'
import { columns } from './components/jobs/columns'
import { DataTable } from './components/jobs/data-table'
import { Card } from './components/ui/card'
import { useVacancy } from './hooks/useVacancy'

interface DetailStore {
    vacancy: Partial<Vacancy>
    setVacancy: (vacancy: Partial<Vacancy>) => void
}

export const useDetailStore = create<DetailStore>()(
    devtools(
        persist(
            (set) => ({
                vacancy: {},
                setVacancy: (vacancy) =>
                    set(() => ({
                        vacancy,
                    })),
            }),
            {
                name: 'jobs-storage',
                storage: createJSONStorage(() => sessionStorage),
                partialize: (state) =>
                    Object.fromEntries(
                        Object.entries(state).filter(
                            ([key]) => !['createdAt', 'updatedat'].includes(key)
                        )
                    ),
            }
        )
    )
)
const App = () => {
    const { data, isLoading } = useVacancy()
    const setVacancy = useDetailStore((state) => state.setVacancy)
    const selectedVacancy = useDetailStore((state) => state.vacancy)

    useEffect(() => {
        if (!data || isLoading) return
        const defaultDetail = R.head(data.allVacancies)
        if (R.isNil(defaultDetail)) return
        setVacancy(defaultDetail)
    }, [data, isLoading, setVacancy])

    if (!data || isLoading) return

    return (
        <ThemeProvider defaultTheme={'dark'} storageKey={'vite-ui-theme'}>
            <div className={'container grid grid-cols-2'}>
                <div className={'max-h-dvh overflow-scroll p-2.5'}>
                    <DataTable columns={columns} data={data.allVacancies} />
                </div>
                {selectedVacancy.description && (
                    <div className={'max-h-dvh p-2.5'}>
                        <Card className={'flex flex-col max-h-full'}>
                            <div
                                className={'flex gap-5 px-5 pt-5 items-center'}
                            >
                                <div
                                    className={
                                        'flex w-12 h-12 items-center justify-center rounded-sm overflow-hidden'
                                    }
                                >
                                    {R.isEmpty(selectedVacancy.companyLogo) ? (
                                        <Building2
                                            className={'h-4 w-4 border'}
                                        />
                                    ) : (
                                        <img
                                            className={'w-full h-full'}
                                            src={selectedVacancy.companyLogo}
                                        />
                                    )}
                                </div>
                                <div className={'flex-col gap-4 items-center'}>
                                    <h2
                                        className={
                                            'text-2xl inline-block font-semibold tracking-tight transition-colors'
                                        }
                                    >
                                        {selectedVacancy.company}
                                    </h2>
                                    <p>{selectedVacancy.title}</p>
                                    <span className={'text-muted-foreground'}>
                                        {selectedVacancy.contractType}
                                    </span>
                                    {selectedVacancy.experienceLevel && (
                                        <span
                                            className={'text-muted-foreground'}
                                        >
                                            &nbsp;&#45;&nbsp;
                                            {selectedVacancy.experienceLevel}
                                        </span>
                                    )}

                                    {selectedVacancy.workplaceType && (
                                        <span
                                            className={'text-muted-foreground'}
                                        >
                                            &nbsp;&#45;&nbsp;
                                            {selectedVacancy.workplaceType}
                                        </span>
                                    )}
                                    {selectedVacancy.location && (
                                        <span
                                            className={'text-muted-foreground'}
                                        >
                                            &nbsp;&#45;&nbsp;
                                            {selectedVacancy.location}
                                        </span>
                                    )}
                                </div>
                            </div>
                            <div
                                className={
                                    'text-sm p-5 overflow-scroll markdown'
                                }
                            >
                                <Markdown>
                                    {selectedVacancy.description}
                                </Markdown>
                            </div>
                        </Card>
                    </div>
                )}
            </div>
        </ThemeProvider>
    )
}

export default App
