<script setup></script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light m-3">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Schedula</a>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="bi bi-calendar"></i> Calendar</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="#"
                            ><i class="bi bi-plus-square"></i> Create</a
                        >
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"
                            ><i class="bi bi-currency-dollar"></i> Billing</a
                        >
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#"><i class="bi bi-person-square"></i> Profile</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
