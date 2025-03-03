<template>
    <div class="card">
        <div class="card-body">
            <h2>User List</h2>
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>List of Users</strong>
                    <p text="text-instructions">
                        The following are a list of users associated to {{destination}}. To add a new user please
                        click on the "Add User" at the bottom of the page.
                    </p>
                </div>
                <div class="col-md-8">
                    <table class="table">
                        <thead>
                            <tr>
                                <td>User</td>
                                <td>Group List</td>
                                <td>Permission List</td>
                                <td>Team Leader</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in localListResults"
                                :key="user.username">
                                <td>
                                    {{user.username__first_name}} {{user.username__last_name}}
                                </td>
                                <td>
                                    {{user.group__group_name}}
                                </td>
                                <td>
                                    {{user.permission_set__permission_set_name}}
                                </td>
                                <td style="text-align: center">
                                    <input class="form-check-input"
                                           type="checkbox"
                                           v-bind:checked="user.group_leader"
                                           v-bind:data-group="user.group"
                                           v-bind:data-permission-set="user.permission_set"
                                           v-bind:data-user="user.username"
                                           v-on:change="updateGroupLeader"
                                    >
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <hr>
            <div class="row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="addUser"
                    >Add User</a>
                </div>
            </div>
        </div>

        <!-- MODALS -->
        <admin-add-user v-bind:destination="destination"
                        v-bind:location-id="locationId"
        ></admin-add-user>
    </div>
</template>

<script>
    import {Modal} from 'bootstrap';
    const axios = require('axios');

    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    //Vue Components
    import AdminAddUser from "./AdminAddUser.vue";

    export default {
        name: "UserList",
        components: {
            AdminAddUser,
        },
        props: {
            destination: {
                type: String,
                default: "",
            },
            locationId: {
                type: Number,
                default: 0,
            },
            userListResults: {
                type: Array, 
                default: function() { 
                    return []; 
                }, 
            },
        },
        data() {
            return {
                localListResults: [],
            }
        },
        methods: {
            addUser: function() {
                //Show the user's modal
                const addUserModal = new Modal(document.getElementById('addUserModal'))
                addUserModal.show();
            },
            isTeamLeader: function(username /* As an ID*/) {
                //Get count of the data from userListResults, where username and group_leader == true
                const count = this.userListResults.filter(row => {
                    return row.username === username && row.group_leader;
                }).length;

                //If length > 0, return true
                return count > 0;
            },
            updateGroupLeader: function(event) {
                //Get if the checkbox is ticked or not
                const group_leader = event.target.checked;

                // Send to the backend
                const data_to_send = new FormData();
                data_to_send.set('group_leader', group_leader);
                data_to_send.set('username', event.target.dataset.user);

                //Case specific data
                if (this.destination === "group" || this.destination === "user") {
                    data_to_send.set("group", event.target.dataset.group);
                } else if (this.destination === "permission_set") {
                    data_to_send.set("permission_set", event.target.dataset.permissionSet);
                }

                axios.post(
                    `/update_group_leader_status/${this.destination}/`,
                    data_to_send,
                ).then(response => {
                    this.localListResults = response.data;
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            }
        },
        mounted() {
            this.localListResults = this.userListResults;
        }
    }
</script>

<style scoped>

</style>