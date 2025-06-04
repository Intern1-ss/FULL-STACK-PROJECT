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
    window.location.href = "/";
}

function showStudentPage() {
    window.location.href = "/students";
}

function showAddStudentPage() {
    window.location.href = "/students/add";
}

function showUploadStudentPage() {
    window.location.href = "/students/upload";
}

function showFacultyPage() {
    window.location.href = "/faculty";
}

function showAddFacultyPage() {
    window.location.href = "/faculty/add";
}

function showUploadFacultyPage() {
    window.location.href = "/faculty/upload";
}

function showDepartmentsPage() {
    window.location.href = "/departments";
}

function showAddDepartmentsPage() {
    window.location.href = "/departments/add";
}

function showUploadDepartmentsPage() {
    window.location.href = "/departments/upload";
}

function showCampusPage() {
    window.location.href = "/campus";
}

function showAddCampusPage() {
    window.location.href = "/campus/add";
}

function showUploadCampusPage() {
    window.location.href = "/campus/upload";
}

function showCampusCard(element) {
        const campusItem = element.closest('.campus-item');
        const content = campusItem.querySelector('.campus-card-content');
        content.classList.toggle('display-none');
}

function showProgramPage() {
    window.location.href = "/programs";
}

function showAddProgramsPage() {
    window.location.href = "/programs/add";
}

function showUploadProgramsPage() {
    window.location.href = "/programs/upload";
}

function closePopup() {
    let popup = document.getElementById('popup');
    popup.classList.add('display-none');
}

function openPopup() {
    let popup = document.getElementById('popup');
    popup.classList.remove('display-none');
}

function menuCollapse(){
    console.log("Menu collapsed");
    let panel = document.querySelectorAll('.right-panel');
    let logoTitle = document.querySelector('.logo-title');
    if (menuOpen) {
        document.querySelectorAll('.icon-name').forEach(el => el.classList.add('display-none'));
        logoTitle.classList.add('display-none');
        document.querySelector('.logo-img').classList.remove('display-none');
        document.querySelector('.menu-panel').classList.add('menu-panel-collapsed');
        document.querySelectorAll('.menu-item').forEach(el => el.classList.add('menu-item-collapsed'));
        menuBackIcon.style.left = "100px";
        panel.forEach(el => { el.style.width = "90vw"; }); 

    } else {
        document.querySelectorAll('.icon-name').forEach(el => el.classList.remove('display-none'));
        logoTitle.classList.remove('display-none');  
        document.querySelector('.logo-img').classList.add('display-none');
        document.querySelector('.menu-panel').classList.remove('menu-panel-collapsed');
        document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('menu-item-collapsed'));
        menuBackIcon.style.left = "280px";
        panel.forEach(el => { el.style.width = "80vw"; });

    }
    menuOpen = !menuOpen;

    const isCollapsed = logoTitle.classList.contains('display-none');
    console.log("Menu collapsed state:", isCollapsed);
    localStorage.setItem('menuCollapsed', isCollapsed ? 'true' : 'false');
}

// document.addEventListener('DOMContentLoaded', () => {
//     const collapsed = localStorage.getItem('menuCollapsed');
//     if(collapsed){
//         menuCollapse();
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const collapsed = localStorage.getItem('menuCollapsed') === 'true';
    if (collapsed) {
        menuOpen = true; 
        menuCollapse();  
    } else {
        menuOpen = false; 
    }
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const yyyy = today.getFullYear();

    const formattedDate = `${dd}-${mm}-${yyyy}`;
    document.getElementById('date').textContent = formattedDate;
});

// this is for the input file drag and drop functionality

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const validTypes = [
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel.sheet.macroEnabled.12',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12'
];

function handleFiles(files) {
    fileList.innerHTML = '';
    Array.from(files).forEach(file => {
    if (!validTypes.includes(file.type)) {
        alert(`File "${file.name}" is not a supported Excel file.`);
        return;
    }
    if (file.size > 50 * 1024 * 1024) {
        alert(`File "${file.name}" exceeds 50MB.`);
        return;
    }

    const item = document.createElement('div');
    item.className = 'file-item';
    item.innerHTML = `<span>${file.name}</span><span class="close-btn" onclick="removeFileItem(this)">×</span>`;
    fileList.appendChild(item);
    }); //this is not working when an item is removed, and when a new item is added, the item is not being created.

    let uploadButton = document.getElementById('uploadButton');
    uploadButton.classList.remove('display-none');

}

function removeFileItem(element) {
    element.parentElement.remove();
    let uploadButton = document.getElementById('uploadButton');
    uploadButton.classList.add('display-none');
}

uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
});

