const format_date = (datetime) => {
    const date = new Date(datetime)
    const date_options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }

    return date.toLocaleDateString('en-SG', date_options)
}

const format_time = (datetime) => {
    const date = new Date(datetime)

    const time_options = {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
        timeZone: 'Asia/Singapore'
    }

    return date.toLocaleTimeString('en-SG', time_options)
}

export { format_date, format_time }
