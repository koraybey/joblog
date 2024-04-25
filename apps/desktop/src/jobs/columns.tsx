'use client'

import type { ColumnDef } from '@tanstack/react-table'
import { MoreHorizontal } from 'lucide-react'

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

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
    uid: string
}

export const columns: ColumnDef<Vacancy>[] = [
    {
        accessorKey: 'company',
        header: 'Company',
        cell: ({ row }) => {
            const job = row.original

            return (
                <div className={'flex gap-4 items-center'}>
                    <img
                        style={{ borderRadius: 4 }}
                        src={job.companyLogo}
                        width={32}
                        height={32}
                    />
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
        accessorKey: 'experienceLevel',
        header: 'Experience',
    },
    {
        accessorKey: 'location',
        header: 'Location',
    },
    {
        accessorKey: 'dateCreated',
        header: 'Created',
    },
    {
        id: 'actions',
        cell: ({ row }) => {
            const job = row.original

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
                        <DropdownMenuItem>Open in browser</DropdownMenuItem>
                        <DropdownMenuItem>Copy link</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>
                            <Button
                                size={'sm'}
                                className={'w-full'}
                                onClick={() =>
                                    void navigator.clipboard.writeText(job.uid)
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
