<template>
    <div>
        <div v-for="customer in customerResults" class="row"
             :key="customer.pk"
        >
            <div class="organisation-details">
                <img v-bind:src="getProfilePicture(customer)"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <div class="organisation-name">
                    <a v-bind:href="`${rootUrl}customer_information/${customer['pk']}/`">
                        {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                    </a>
                </div>
                <div class="organisation-email">
                    <Icon v-bind:icon="icons.mailIcon"></Icon> Email:
                    <a v-bind:href="`mailto:${customer['fields']['customer_email']}`">
                        {{customer['fields']['customer_email']}}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //Mixin
    import iconMixin from "../../mixins/iconMixin";
    import { Icon } from '@iconify/vue';

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "ListCustomers",
        components: {
            Icon,
        },
        props: {
            customerResults: {
                type: Array,
                default: function() {
                    return [];
                },
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        mixins: [
            iconMixin
        ],
        methods: {
            getProfilePicture: function(customer) {
                const image = customer['fields']['customer_profile_picture'];

                //If customer profile is blank - return default picture
                if (image === '' || image === null) {
                    return `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;
                }

                return `${this.rootUrl}private/${image}`;
            }
        }
    }
</script>

<style scoped>

</style>
