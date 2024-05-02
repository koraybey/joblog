'use client'

import type {
    ColumnDef,
    ColumnFiltersState,
    SortingState,
} from '@tanstack/react-table'
import {
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from '@tanstack/react-table'
import { useState } from 'react'

import { Vacancy } from '@/__generated__/gql/graphql'
import { useDetailStore } from '@/App'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'

import { Button } from '../ui/button'
import { Input } from '../ui/input'

interface DataTableProperties<TData, TValue> {
    columns: ColumnDef<TData, TValue>[]
    data: TData[]
}

export const DataTable = <TData, TValue>({
    columns,
    data,
}: DataTableProperties<TData, TValue>) => {
    const setVacancy = useDetailStore((state) => state.setVacancy)

    const [sorting, setSorting] = useState<SortingState>([])
    const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        onSortingChange: setSorting,
        getSortedRowModel: getSortedRowModel(),
        onColumnFiltersChange: setColumnFilters,
        getFilteredRowModel: getFilteredRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        state: {
            sorting,
            columnFilters,
        },
    })

    return (
        <div className={'w-full'}>
            <div className={'flex items-center pb-4'}>
                <Input
                    placeholder={'Search for a company...'}
                    value={
                        (table
                            .getColumn('company')
                            ?.getFilterValue() as string) ?? ''
                    }
                    // eslint-disable-next-line react/jsx-no-bind
                    onChange={(event) =>
                        table
                            .getColumn('company')
                            ?.setFilterValue(event.target.value)
                    }
                    className={'max-w-full'}
                />
            </div>
            <div className={'rounded-md border'}>
                <Table>
                    <TableHeader>
                        {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow key={headerGroup.id}>
                                {headerGroup.headers.map((header) => {
                                    return (
                                        <TableHead key={header.id}>
                                            {header.isPlaceholder
                                                ? undefined
                                                : flexRender(
                                                      header.column.columnDef
                                                          .header,
                                                      header.getContext()
                                                  )}
                                        </TableHead>
                                    )
                                })}
                            </TableRow>
                        ))}
                    </TableHeader>
                    <TableBody>
                        {table.getRowModel().rows?.length ? (
                            table.getRowModel().rows.map((row) => (
                                <TableRow
                                    key={row.id}
                                    // eslint-disable-next-line react/jsx-no-bind
                                    onClick={() =>
                                        setVacancy(row?.original as Vacancy)
                                    }
                                    data-state={
                                        row.getIsSelected() && 'selected'
                                    }
                                >
                                    {row.getVisibleCells().map((cell) => (
                                        <TableCell key={cell.id}>
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext()
                                            )}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell
                                    colSpan={columns.length}
                                    className={'h-24 text-center'}
                                >
                                    No results.
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            <div className={'flex items-center justify-end space-x-2 py-4'}>
                <Button
                    variant={'outline'}
                    size={'sm'}
                    // eslint-disable-next-line react/jsx-no-bind
                    onClick={() => table.previousPage()}
                    disabled={!table.getCanPreviousPage()}
                >
                    Previous
                </Button>
                <Button
                    variant={'outline'}
                    size={'sm'}
                    // eslint-disable-next-line react/jsx-no-bind
                    onClick={() => table.nextPage()}
                    disabled={!table.getCanNextPage()}
                >
                    Next
                </Button>
            </div>
        </div>
    )
}
