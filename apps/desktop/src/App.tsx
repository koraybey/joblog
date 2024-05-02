import { Building2, X } from 'lucide-react'
import * as R from 'ramda'
import Markdown from 'react-markdown'
import { create } from 'zustand'
import { createJSONStorage, devtools, persist } from 'zustand/middleware'

import { ThemeProvider } from '@/components/theme-provider'

import { Vacancy } from './__generated__/gql/graphql'
import { columns } from './components/jobs/columns'
import { DataTable } from './components/jobs/data-table'
import { Button } from './components/ui/button'
import { useVacancy } from './hooks/useVacancy'

interface DetailStore {
    vacancy: Partial<Vacancy>
    setVacancy: (vacancy: Partial<Vacancy> | undefined) => void
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
                                ![
                                    'dateCreated',
                                    'dateUpdated',
                                    'description',
                                ].includes(key)
                        )
                    ),
            }
        )
    )
)
const App = () => {
    const { data, isLoading } = useVacancy()
    const selectedVacancy = useDetailStore((state) => state.vacancy)
    const setVacancy = useDetailStore((state) => state.setVacancy)

    if (!data || isLoading) return

    return (
        <ThemeProvider defaultTheme={'dark'} storageKey={'vite-ui-theme'}>
            <div className={'container max-h-svh'}>
                <div>
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
                {selectedVacancy?.description ? (
                    <div
                        className={
                            'absolute w-1/2 right-0 top-0 bottom-0 bg-background text-sm max-h-full markdown overflow-scroll border-l'
                        }
                    >
                        <div
                            className={
                                'flex justify-between items-center pt-5 px-5'
                            }
                        >
                            <div className={'flex gap-4 items-center'}>
                                <div
                                    className={
                                        'flex w-9 h-9 items-center justify-center rounded-sm overflow-hidden'
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
                                            {selectedVacancy.experienceLevel}
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
                            <Button
                                variant={'outline'}
                                className={'h-8 w-8 p-0'}
                                onClick={() => setVacancy(undefined)}
                            >
                                <span className={'sr-only'}>Open menu</span>
                                <X className={'h-4 w-4'} />
                            </Button>
                        </div>
                        <div className={'p-4'}>
                            <Markdown>{selectedVacancy.description}</Markdown>
                        </div>
                    </div>
                ) : undefined}
            </div>
        </ThemeProvider>
    )
}

export default App
