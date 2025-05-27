let overview = document.getElementById("overview-item");
let students = document.getElementById("students-item");
let courses = document.getElementById("courses-item");
let departments = document.getElementById("departments-item");
let faculty = document.getElementById("faculty-item");
let campus = document.getElementById("campus-item");
let studentPage = document.getElementById("studentPage");
let addStudentPage = document.getElementById("addStudentPage");
let overviewPage = document.getElementById("overviewPage");
let coursePage = document.getElementById("coursePage");
let departmentsPage = document.getElementById("departmentsPage");
let addDepartmentsPage = document.getElementById("addDepartmentsPage");
let facultyPage = document.getElementById("facultyPage");
let addFacultyPage = document.getElementById("addFacultyPage");
let campusPage = document.getElementById("campusPage");
let menuBackIcon = document.getElementById("backIcon");
let menuOpen = true;




function showOverviewPage() {
    overviewPage.style.display = "flex";
    studentPage.style.display = "none";
    addStudentPage.style.display = "none";
    facultyPage.style.display = "none";
    addFacultyPage.style.display = "none";
    departmentsPage.style.display = "none";
    addDepartmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";

    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    overview.classList.add('active');
}

function showStudentPage() {
    studentPage.style.display = "block";
    addStudentPage.style.display = "none";
    overviewPage.style.display = "none";
    facultyPage.style.display = "none";
    addFacultyPage.style.display = "none";
    departmentsPage.style.display = "none";
    addDepartmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";

    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    students.classList.add('active');
}

function showAddStudentPage() {
    addStudentPage.style.display = "block";
    overviewPage.style.display = "none";
    studentPage.style.display = "none";
    facultyPage.style.display = "none";
    addFacultyPage.style.display = "none";
    departmentsPage.style.display = "none";
    addDepartmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";
}

function showFacultyPage() {
    facultyPage.style.display = "block";
    addFacultyPage.style.display = "none";
    overviewPage.style.display = "none";
    studentPage.style.display = "none";
    addStudentPage.style.display = "none";
    departmentsPage.style.display = "none";
    addDepartmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";

    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    faculty.classList.add('active');
}

function showAddFacultyPage() {
    addFacultyPage.style.display = "block";
    overviewPage.style.display = "none";
    studentPage.style.display = "none";
    addStudentPage.style.display = "none";
    facultyPage.style.display = "none";
    departmentsPage.style.display = "none";
    addDepartmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";
}

function showDepartmentsPage() {
    departmentsPage.style.display = "block";
    addDepartmentsPage.style.display = "none";
    overviewPage.style.display = "none";
    studentPage.style.display = "none";
    addStudentPage.style.display = "none";
    facultyPage.style.display = "none";
    addFacultyPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";

    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    departments.classList.add('active');
}

function showAddDepartmentsPage() {
    addDepartmentsPage.style.display = "block";
    overviewPage.style.display = "none";
    studentPage.style.display = "none";
    addStudentPage.style.display = "none";
    facultyPage.style.display = "none";
    addFacultyPage.style.display = "none";
    departmentsPage.style.display = "none";
    // coursePage.style.display = "none";
    // campusPage.style.display = "none";
}

function menuCollapse(){
    console.log("Menu collapsed");
    let panel = document.querySelectorAll('.right-panel');
    if (menuOpen) {
        document.querySelectorAll('.icon-name').forEach(el => el.classList.add('display-none'));
        document.querySelector('.logo-title').classList.add('display-none');
        document.querySelector('.logo-img').classList.remove('display-none');
        document.querySelector('.menu-panel').classList.add('menu-panel-collapsed');
        document.querySelectorAll('.menu-item').forEach(el => el.classList.add('menu-item-collapsed'));
        menuBackIcon.style.left = "100px";
        panel.forEach(el => { el.style.width = "90vw"; }); 

    } else {
        document.querySelectorAll('.icon-name').forEach(el => el.classList.remove('display-none'));
        document.querySelector('.logo-title').classList.remove('display-none');  
        document.querySelector('.logo-img').classList.add('display-none');
        document.querySelector('.menu-panel').classList.remove('menu-panel-collapsed');
        document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('menu-item-collapsed'));
        menuBackIcon.style.left = "280px";
        panel.forEach(el => { el.style.width = "80vw"; });

    }
    menuOpen = !menuOpen;
}