import { ref } from 'vue'
import Comment from 'components/Comment.js'

export default {
	components: {
		Comment
	},
	setup() {
		const loading = ref(true)
		const comments = ref([])
		const newComment = ref('')

		const updateComments = () => {
			fetch('/api/comments')
				.then(response => response.json())
				.then(data => {
					comments.value = data
					loading.value = false
					const commentsEl = document.querySelector('#comments')
					setTimeout(() => {
						commentsEl.scrollTo(0, commentsEl.scrollHeight)
					}, 150)
				})
		}

		const postComment = () => {
			const data = {
				'content': newComment.value
			}
			newComment.value = ''
			
			fetch('/api/comment', {
				method: 'post',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			})
				.then(() => updateComments())
				.catch(() => { alert('Une erreur est survenue...') })
		}

		const getFlag = () => {
			fetch('/api/flag')
				.then(response => response.text())
				.then(alert)
				.catch(() => { alert('Une erreur est survenue...') })
		}

		updateComments()
		return { loading, comments, newComment, postComment, getFlag }
	},
	template: `
	<nav class="navbar is-black" role="navigation" aria-label="main navigation">
		<div class="navbar-brand">
			<a class="navbar-item" href="/">
				<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64px" height="64px" viewBox="0 0 64 64" aria-hidden="true" fill="#ffffff" stroke="#ffffff" transform="matrix(1, 0, 0, 1, 0, 0)">
					<path d="M56 25.902c-2.864-7.742-5.73-15.484-8.598-23.226c-15.84-4.854-21.363 18.166-37.205 13.312L8 16.776L24.744 62h2.488l-8.437-22.786l.001.002C34.639 44.067 40.161 21.049 56 25.902" fill="#ffffff"/>
				</svg>
				<h3 class="title is-5 ml-2">FlagForum</h3>
			</a>
		</div>
		<div class="navbar-end">
			<div class="navbar-item">
				<div class="buttons">
					<a class="button is-danger" @click="getFlag">
						<strong>Obtenir le flag</strong>
					</a>
				</div>
			</div>
		</div>
	</nav>

	<section class="section level">
		<div class="level-item has-text-centered">
			<div>
				<p class="heading">Bienvenue sur</p>
				<p class="title">Le forum illicite de la CYBN</p>
			</div>
		</div>
	</section>

	<div id="comments" class="block container is-max-widescreen">
		<div v-if="loading">loading</div>
		<template v-else>
			<Comment v-for="(comment, index) in comments" :key="index" :comment="comment"/>
		</template>
	</div>
	<form id="form" class="container is-max-widescreen" @submit.prevent="postComment">
		<input v-model="newComment" class="input" type="text" placeholder="Ajoutez un commentaire" />
	</form>
	`
}