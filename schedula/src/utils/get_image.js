function getImageUrl(url) {
    // Need to check if event.image !== None is necessary
    try {
        return `https://spickbucket.s3.ap-southeast-1.amazonaws.com/${url}`
    } catch (error) {
        return '../../public/default.png'
    }

    // Return a default image URL or an empty string if event or event.image is not available
}

export { getImageUrl }
