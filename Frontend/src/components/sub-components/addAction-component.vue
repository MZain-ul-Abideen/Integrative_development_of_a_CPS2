<template>
    <div class="add-action-wrapper">
        <div class="add-action-div">
            <form action="" class="mt-4">
                <input type="text" class="text-feild" placeholder="Enter Action Name">
                <textarea name="discription" id="discription" class="discription-feild" placeholder="Enter Action Discription"></textarea>
                <button class="button-2 my-3">Add</button>
            </form>
        </div>
    </div>
</template>

<script setup></script>

<style scoped>
.add-action-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}
.add-action-div {
    display: flex;
    flex-direction: column;
    width: 50%;
    justify-content: center;
    align-items: center;
}
</style>