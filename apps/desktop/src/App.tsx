import { Building2 } from 'lucide-react'
import * as R from 'ramda'
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
                            ([key]) =>
                                !['dateCreated', 'dateUpdated'].includes(key)
                        )
                    ),
            }
        )
    )
)
const App = () => {
    const { data, isLoading } = useVacancy()
    const selectedVacancy = useDetailStore((state) => state.vacancy)

    if (!data || isLoading) return

    return (
        <ThemeProvider defaultTheme={'dark'} storageKey={'vite-ui-theme'}>
            <div className={'container grid grid-cols-2 gap-4'}>
                <div className={'max-h-dvh col-span-1'}>
                    <div
                        className={
                            'flex flex-row justify-between items-center px-3 h-24'
                        }
                    >
                        <h2
                            className={
                                'text-3xl font-semibold transition-colors'
                            }
                        >
                            Vacancies
                        </h2>
                        <h2
                            className={
                                'text-3xl font-semibold text-muted-foreground transition-colors'
                            }
                        >
                            {data.allVacancies.length}
                        </h2>
                    </div>
                    <div className={'max-h-full overflow-auto'}>
                        <DataTable columns={columns} data={data.allVacancies} />
                    </div>
                </div>
                {selectedVacancy.description && (
                    <div className={'max-h-dvh col-span-1'}>
                        <div
                            className={
                                'flex flex-row justify-between items-center px-3 h-24'
                            }
                        >
                            <h2
                                className={
                                    'text-3xl font-semibold transition-colors'
                                }
                            >
                                Details
                            </h2>
                        </div>
                        <div
                            className={
                                'text-sm markdown max-h-full overflow-auto'
                            }
                        >
                            <Card>
                                <div
                                    className={
                                        'flex gap-4 items-center pt-5 px-5'
                                    }
                                >
                                    <div
                                        className={
                                            'flex w-9 h-9 items-center justify-center rounded-sm overflow-hidden'
                                        }
                                    >
                                        {R.isEmpty(
                                            selectedVacancy.companyLogo
                                        ) ? (
                                            <Building2
                                                className={'h-4 w-4 border'}
                                            />
                                        ) : (
                                            <img
                                                className={'w-full h-full'}
                                                src={
                                                    selectedVacancy.companyLogo
                                                }
                                            />
                                        )}
                                    </div>
                                    <div
                                        className={
                                            'flex-col gap-4 items-center'
                                        }
                                    >
                                        <h4
                                            className={
                                                'font-medium transition-colors'
                                            }
                                        >
                                            {selectedVacancy.company}
                                        </h4>
                                        <h2 className={'transition-colors'}>
                                            {selectedVacancy.title}
                                        </h2>
                                        <span
                                            className={
                                                'text-xs text-muted-foreground'
                                            }
                                        >
                                            {selectedVacancy.contractType}
                                        </span>
                                        {selectedVacancy.experienceLevel && (
                                            <span
                                                className={
                                                    'text-xs text-muted-foreground'
                                                }
                                            >
                                                &nbsp;&#45;&nbsp;
                                                {
                                                    selectedVacancy.experienceLevel
                                                }
                                            </span>
                                        )}
                                        {selectedVacancy.workplaceType && (
                                            <span
                                                className={
                                                    'text-xs text-muted-foreground'
                                                }
                                            >
                                                &nbsp;&#45;&nbsp;
                                                {selectedVacancy.workplaceType}
                                            </span>
                                        )}
                                        {selectedVacancy.location && (
                                            <span
                                                className={
                                                    'text-xs text-muted-foreground'
                                                }
                                            >
                                                &nbsp;&#45;&nbsp;
                                                {selectedVacancy.location}
                                            </span>
                                        )}
                                    </div>
                                </div>
                                <div className={'p-4'}>
                                    <Markdown>
                                        {selectedVacancy.description}
                                    </Markdown>
                                </div>
                            </Card>
                        </div>
                    </div>
                )}
            </div>
        </ThemeProvider>
    )
}

export default App
