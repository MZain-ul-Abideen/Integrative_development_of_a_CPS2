<template>
    <div class="add-trigger-wrapper">
        <div class="add-trigger-div">
            <form action="" class="mt-4">
                <input type="text" class="text-feild" placeholder="Enter Trigger Name">
                <textarea name="discription" id="discription" class="discription-feild" placeholder="Enter Trigger Discription"></textarea>
                <button class="button-2 my-3">Add</button>
            </form>
        </div>
    </div>
</template>

<script setup></script>

<style scoped>
.add-trigger-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
}
.add-trigger-div {
    display: flex;
    flex-direction: column;
    width: 50%;
    justify-content: center;
    align-items: center;
}
</style>