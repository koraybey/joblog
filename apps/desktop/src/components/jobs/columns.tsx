/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import type { ColumnDef } from '@tanstack/react-table'
import { Building2, MoreHorizontal } from 'lucide-react'
import * as R from 'ramda'

import type { Vacancy } from '@/__generated__/gql/graphql'
import { useDetailStore } from '@/App'
import { Button } from '@/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { deleteVacancy } from '@/hooks/useDeleteVacancy'
import { formatDateRelative } from '@/lib/utils'

export const columns: ColumnDef<Vacancy>[] = [
    {
        accessorKey: 'company',
        header: 'Company',
        cell: ({ row }) => {
            const job = row.original

            return (
                <div className={'flex gap-4 items-center'}>
                    <div
                        className={
                            'flex w-9 h-9 items-center justify-center rounded-sm overflow-hidden'
                        }
                    >
                        {R.isEmpty(job.companyLogo) ? (
                            <Building2 className={'h-4 w-4 border'} />
                        ) : (
                            <img
                                className={'w-full h-full '}
                                src={job.companyLogo}
                            />
                        )}
                    </div>
                    <span>{job.company}</span>
                </div>
            )
        },
    },
    {
        accessorKey: 'title',
        header: 'Title',
    },
    {
        accessorKey: 'location',
        header: 'Location',
    },
    {
        accessorKey: 'dateCreated',
        header: 'Created',
        cell: ({ row }) => {
            const job = row.original
            // codegen generates wrong scalar types because it does not recognize chrono::NaiveDateTime types.
            // TODO Fix createdAt and updatedAt types on db
            // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
            const date = formatDateRelative(job?.dateCreated)
            return <span className={'capitalize::first-letter'}>{date}</span>
        },
    },
    {
        id: 'actions',
        cell: ({ row }) => {
            const job = row.original
            const setVacancy = useDetailStore.getState().setVacancy

            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant={'outline'} className={'h-8 w-8 p-0'}>
                            <span className={'sr-only'}>Open menu</span>
                            <MoreHorizontal className={'h-4 w-4'} />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align={'end'}>
                        <DropdownMenuLabel>Mark as</DropdownMenuLabel>
                        <DropdownMenuItem>Rejected</DropdownMenuItem>
                        <DropdownMenuItem>Withdrawn</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => void setVacancy(job)}>
                            View
                        </DropdownMenuItem>
                        <DropdownMenuItem
                            onClick={() => void window.open(job.url)}
                        >
                            Open link
                        </DropdownMenuItem>
                        <DropdownMenuItem
                            onClick={() =>
                                void navigator.clipboard.writeText(job.url)
                            }
                        >
                            Copy link
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>
                            <Button
                                size={'sm'}
                                className={'w-full'}
                                // eslint-disable-next-line react/jsx-no-bind
                                onClick={() =>
                                    void deleteVacancy({ uid: job.uid })
                                }
                                variant={'destructive'}
                            >
                                Delete
                            </Button>
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]
