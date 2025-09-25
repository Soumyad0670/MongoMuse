document.getElementById("userForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const user = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        age: parseInt(document.getElementById("age").value)
    };

    fetch("/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    })
    .then(res => res.json())
    .then(data => {
        alert("User created with ID: " + data.id);
        loadUsers();
    });
});

function loadUsers() {
    fetch("/users")
        .then(res => res.json())
        .then(users => {
            const list = document.getElementById("userList");
            list.innerHTML = "";
            users.forEach(user => {
                const li = document.createElement("li");
                li.textContent = `${user.name} (${user.email}, ${user.age})`;
                list.appendChild(li);
            });
        });
}

window.onload = loadUsers;
