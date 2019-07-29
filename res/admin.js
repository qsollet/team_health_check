var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        flipped: false,
        current_question: 0,
        page: 'init', // init, question, results
        room: '',
        invalid_room: '',
        results: [], // All results
        votes: {}, // Results for current question
        result: {
            'R': 0,
            'A': 0,
            'G': 0,
        },
        result_class: '',
        nb_votes: 0,
    },
    methods: {
        check_ready: function() {
            this.room = this.room.toLowerCase()
            if (this.room == '') {
                this.invalid_room = 'Need a room name'
            } else {
                this.invalid_room = ''
                this.page = 'question'
                this.refresh()
            }
        },
        next_q: function() {
            this.flipped = false
            this.set_current_question(this.current_question + 1)
        },
        previous_q: function() {
            this.flipped = false
            if (this.current_question <= 0) {
                return
            }
            this.set_current_question(this.current_question - 1)
        },
        flip: function() {
            this.flipped = !this.flipped
        },
        update_result: function() {
            this.votes = this.results[this.current_question]
            // reset result
            this.result = {'R': 0, 'A': 0, 'G': 0}
            // calculate total for each color
            for (var i in this.votes) {
                this.result[this.votes[i].vote]++
            }
            // calculate overall color
            this.nb_votes = this.result['R'] + this.result['A'] + this.result['G']
            var c = 'W'
            if (this.nb_votes > 0) {
                c = this.get_overall_class(this.result['R'], this.result['A'], this.result['G'])
            } else {
                // If no result, unflip (usually means reset by other admin)
                this.flipped = false
            }
            this.result_class = 'bg-' + c
        },
        build_result_page: function() {
            data = []
            for (var i = 0; i < this.results.length; i++) {
                var r = 0
                var a = 0
                var g = 0
                for (var j in this.results[i]) {
                    if (this.results[i][j].vote == 'R') {
                        r++
                    } else if (this.results[i][j].vote == 'A') {
                        a++
                    } else if (this.results[i][j].vote == 'G') {
                        g++
                    }
                }
                data.push({
                    'question': i + 1,
                    'votes': Object.keys(this.results[i]).length,
                    'red': r,
                    'amber': a,
                    'green': g,
                    'overall': this.get_overall_class(r, a, g)
                })
            }
            return data
        },
        get_overall_class: function(r, a, g) {
            var q = r * 3 + a * 2 + g
            var d = r + a + g

            if (d == 0) {
                return ''
            }
            if (q / d > 2.34) {
                return 'R'
            }
            if (q / d > 1.67) {
                return 'A'
            }
            return 'G'
        },
        refresh: function() {
            if (this.page == 'init') {
                return
            }
            $.get('/ws/admin/r/' + this.room, function(data) {
                // Save vote
                app.results = data.votes
                app.current_question = data.current_question
                // update result
                app.update_result()
            }, 'json')
        },
        set_current_question: function(index) {
            $.post('/ws/admin/set_q/' + this.room, {'index': index}, function() {
                app.refresh()
            })
        },
        see_results: function() {
            this.page = 'results'
        },
        see_questions: function() {
            this.page = 'question'
        },
    }
})

setInterval(function() {
    app.refresh()
}, 2000)
