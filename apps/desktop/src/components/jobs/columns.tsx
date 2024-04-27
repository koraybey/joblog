import type { ColumnDef } from '@tanstack/react-table'
import clsx from 'clsx'
import { Building2, MoreHorizontal } from 'lucide-react'
import * as R from 'ramda'

import type { Vacancy } from '@/__generated__/gql/graphql'
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
import { updateVacancy } from '@/hooks/useUpdateVacancy'
import { copyToClipboard, openUrl } from '@/hooks/utils'
import { formatDateRelative } from '@/lib/utils'

const del = (uid: string) => () => void deleteVacancy({ uid })
const setStatus = (uid: string, status: string) => () =>
    void updateVacancy({ uid, status })

type StatusProps = { status: string; text: string; background: string }

const status: StatusProps[] = [
    { status: 'Rejected', text: 'text-red-500', background: 'bg-red-500' },
    {
        status: 'Withdrawn',
        text: 'text-purple-500',
        background: 'bg-purple-500',
    },
    { status: 'Applied', text: 'text-green-500', background: 'bg-green-500' },
    {
        status: 'Interviewing',
        text: 'text-blue-500',
        background: 'bg-blue-500',
    },
    { status: 'Created', text: 'text-white', background: 'bg-white' },
]

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
                                className={'w-full h-full'}
                                src={job.companyLogo}
                            />
                        )}
                    </div>
                    <span className={'font-medium'}>{job.company}</span>
                </div>
            )
        },
    },
    {
        accessorKey: 'title',
        header: 'Title',
    },
    {
        accessorKey: 'dateModified',
        header: 'Updated',
        cell: ({ row }) => {
            const job = row.original
            // codegen generates wrong scalar types because it does not recognize chrono::NaiveDateTime types.
            // TODO Fix createdAt and updatedAt types on db
            // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
            const date = formatDateRelative(job?.dateModified)
            return <span className={'capitalize::first-letter'}>{date}</span>
        },
    },
    {
        accessorKey: 'status',
        header: 'Status',
        cell: ({ row }) => {
            const job = row.original
            const style = status?.find((s) => s.status === row.original.status)
            return (
                <div
                    className={clsx(
                        'flex flex-row items-center font-medium',
                        style?.text
                    )}
                    key={job.description}
                >
                    <div
                        className={clsx(
                            'w-2 h-2 rounded mr-1.5',
                            style?.background
                        )}
                    ></div>
                    {job.status}
                </div>
            )
        },
    },
    {
        id: 'actions',
        cell: ({ row }) => {
            const job = row.original
            return (
                <div className={'flex flex-row gap-2'}>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button
                                variant={'outline'}
                                className={'h-8 w-8 p-0'}
                            >
                                <span className={'sr-only'}>Open menu</span>
                                <MoreHorizontal className={'h-4 w-4'} />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                            className={'font-medium'}
                            align={'end'}
                        >
                            <DropdownMenuLabel
                                className={'text-muted-foreground'}
                            >
                                Actions
                            </DropdownMenuLabel>
                            <DropdownMenuItem onClick={openUrl(job.url)}>
                                Open Link
                            </DropdownMenuItem>
                            <DropdownMenuItem
                                onClick={copyToClipboard(job.url)}
                            >
                                Copy link
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuLabel
                                className={'text-muted-foreground'}
                            >
                                Mark as
                            </DropdownMenuLabel>
                            {status.map((status: StatusProps) => (
                                <DropdownMenuItem
                                    key={status.status}
                                    onClick={setStatus(
                                        job.uid,
                                        status.status.trim()
                                    )}
                                >
                                    <div
                                        className={clsx(
                                            'flex flex-row items-center font-medium',
                                            status.text
                                        )}
                                        key={job.description}
                                    >
                                        <div
                                            className={clsx(
                                                'w-2 h-2 rounded mr-1',
                                                status.background
                                            )}
                                        ></div>
                                        {status.status}
                                    </div>
                                </DropdownMenuItem>
                            ))}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={del(job.uid)}
                                className={'text-red-500 focus:text-red-500'}
                            >
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            )
        },
    },
]
