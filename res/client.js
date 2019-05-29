// Votes can be : R, A, G
// Vuejs app
var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        name: '',
        room: '',
        not_ready: true,
        invalid_name: '',
        invalid_room: '',
    },
    methods: {
        check_ready: function() {
            if (this.name == '') {
                this.invalid_name = 'Need to enter a name'
            } else {
                this.invalid_name = ''
            }
            if (this.room == '') {
                this.invalid_room = 'Need to enter a room id'
            } else {
                this.invalid_room = ''
            }
            if (this.name != '' && this.room != '') {
                this.not_ready = false
            }
        },
        unready: function() {
            this.not_ready = true
        },
        vote: function(vote) {
            this.sendVote(vote)
        },
        setVote: function(vote) {
            // Reset vote
            $('.voted').removeClass('voted')
            // set vote
            switch (vote) {
                case 'R':
                    $('.red').addClass('voted')
                    break;
                case 'A':
                    $('.amber').addClass('voted')
                    break;
                case 'G':
                    $('.green').addClass('voted')
                    break;
            }
        },
        sendVote: function(vote) {
            if (this.not_ready) {
                return
            }
            $.post('/ws/vote/' + this.room, {"vote": vote, "name": this.name}, function(data) {
                app.setVote(data)
            })
        },
        getVote: function() {
            if (this.not_ready) {
                return
            }
            $.get('/ws/vote/' + this.room, function(data) {
                app.setVote(data)
            })
        }
    },
})

// Refresh timer
setInterval(function() {
    app.getVote()
}, 2000)
