import { ref, computed } from 'vue'

export default {
	props: {
		comment: Object,
	},
	setup(props) {
		const content = ref('')
		const now = ref(Date.now())
		setInterval(function () {
			now.value = Date.now()
		}, 1000)
		const date = computed(() => {
			let delta = Math.ceil((now.value - props.comment.date) / 1000)
			if (delta < 60) return `${delta}s`
			delta = Math.ceil(delta / 60)
			if (delta < 60) return `${delta}m`
			delta = Math.ceil(delta / 60)
			if (delta < 24) return `${delta}h`
			return new Date(props.comment.date)
		})
		fetch('/public/data/' + props.comment.content_id)
			.then(response => {
				if (!response.ok) throw Error('Unreachable')
				return response.text()
			})
			.then(data => { content.value = data })
			.catch(() => {content.value = 'Impossible de charger le commentaire...'})
		return {
			comment: props.comment,
			content,
			date
		}
	},
	template: `
<article class="media">
	<figure class="media-left">
		<p class="image is-64x64">
			<img :src="'/public/images/' + comment.profile_picture + '.png'" />
		</p>
	</figure>
	<div class="media-content">
		<div class="content">
			<p>
				<strong>{{comment.author}}</strong><small> · {{date}}</small>
				<br />
				{{content}}
				<br />
			</p>
		</div>
	</div>
</article>

	`
}