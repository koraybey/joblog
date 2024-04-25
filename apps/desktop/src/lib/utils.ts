import { type ClassValue, clsx } from 'clsx'
import { formatRelative, fromUnixTime } from 'date-fns'
import { enGB } from 'date-fns/locale/en-GB'
import { twMerge } from 'tailwind-merge'

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs))

// https://date-fns.org/docs/I18n-Contribution-Guide#formatrelative
// https://github.com/date-fns/date-fns/blob/master/src/locale/en-US/_lib/formatRelative/index.js
// https://github.com/date-fns/date-fns/issues/1218
// https://stackoverflow.com/questions/47244216/how-to-customize-date-fnss-formatrelative
const formatRelativeLocale: { [key: string]: string } = {
    lastWeek: "'Last' eeee 'at' p",
    yesterday: "'Yesterday at' p",
    today: 'p',
    tomorrow: "'Tomorrow at' p",
    nextWeek: "eeee 'at' p",
    other: 'P',
}

export const formatDateRelative = (time: number) =>
    formatRelative(fromUnixTime(time), new Date(), {
        locale: {
            ...enGB,
            formatRelative: (token: string) => formatRelativeLocale[token],
        },
    })
