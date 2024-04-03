function getImageUrl(url) {
    // Need to check if event.image !== None is necessary
    try {
        if (url === null) {
            return 'https://source.unsplash.com/black-dog-wearing-blue-denim-collar-K4mSJ7kc0As'
        }
        return `https://spickbucket.s3.ap-southeast-1.amazonaws.com/${url}`
    } catch (error) {
        return 'https://source.unsplash.com/black-dog-wearing-blue-denim-collar-K4mSJ7kc0As'
    }

    // Return a default image URL or an empty string if event or event.image is not available
}

export { getImageUrl }
