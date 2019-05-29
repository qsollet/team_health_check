var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        flipped: false,
        room: '',
        not_ready: true,
        invalid_room: '',
        votes: {},
        result: {
            'R': 0,
            'A': 0,
            'G': 0,
        },
    },
    methods: {
        check_ready: function() {
            if (this.room == '') {
                this.invalid_room = 'Need a room name'
            } else {
                this.invalid_room = ''
                this.not_ready = false
                this.refresh()
            }
        },
        unready: function() {
            this.not_ready = true
        },
        flip: function() {
            this.flipped = !this.flipped
            if (this.flipped) {
                $('.vote').removeClass('bg-grey')
            } else {
                $('.vote').addClass('bg-grey')
            }
            // var r = data['R'] * 3 + data['A'] * 2 + data['G']
        },
        update_result: function() {
            // reset result
            this.result = {'R': 0, 'A': 0, 'G': 0}
            // calculate result
            for (var i in this.votes) {
                this.result[this.votes[i].vote]++
            }
            // calculate total
            var q = this.result['R'] * 3 + this.result['A'] * 2 + this.result['G']
            var d = this.result['R'] + this.result['A'] + this.result['G']
            var c = 'W'
            if (d > 0) {
                var c = 'R'
                if (q / d < 2.34) {
                    c = 'A'
                }
                if (q / d < 1.67) {
                    c = 'G'
                }
            }
            $('.overall').removeClass('bg-R bg-A bg-G').addClass('bg-' + c)
        },
        reset: function() {
            if (this.not_ready) {
                return
            }
            $.get('/ws/reset/' + this.room)
            this.flipped = true
            this.flip()
        },
        refresh: function() {
            if (this.not_ready) {
                return
            }
            $.get('/ws/admin/' + this.room, function(data) {
                // Save vote
                app.votes = data
                // update result
                app.update_result()
            }, 'json')
        }
    }
})

setInterval(function() {
    app.refresh()
}, 2000)
