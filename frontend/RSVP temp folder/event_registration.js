const inv = Vue.createApp({
    data() {
        return {
            links: {
                home: "../index.php ",
                lists: "./ShoppingList.php",
                inventory: "./Inventory.php",
                recipe: "./RecipeList.php",
                profile: "./Profile.php",
                login: "./login.php",
                logout: "../../server/controller/logout.php",
                register: "./register.php",
            },
            item: "",
            qty: "",
            expiry: "",
            category: "",
        }
    },
    methods: {
        submit() {
            let success = addToInv(this.item, this.qty, this.expiry, this.category)
            this.item = ""
            this.qty = ""
            this.expiry = ""
            this.category = ""
        }
    }
}).mount("#main")

function decline(){
    axios.post("localhost/")
}

var decline = document.getElementById("decline")
decline.addEventListener("onclick", decline())