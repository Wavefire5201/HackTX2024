function scrapeCourseData() {
    // Implement your scraping logic here
    let courses = [];
    // Example: collect course names and IDs from the DOM
    document.querySelectorAll('.course-name-selector').forEach(course => {
        courses.push({
            id: course.getAttribute('data-course-id'),
            name: course.innerText
        });
    });
    return courses;
}
