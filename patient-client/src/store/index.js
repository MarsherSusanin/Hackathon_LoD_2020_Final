import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

const api = 'http://35.226.48.61/api/1.0'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    sessionId: null,
    user: {
      name: 'Петр',
      middlename: 'Петрович'
    },
    anamnesis: {}
  },
  mutations: {
    setSessionId (state, { session_id: sessionId }) {
      state.sessionId = sessionId
    },

    setUserData (state, payload) {
      state.user = payload
    },

    setUserAnamnesis (state, payload) {
      Object.assign(state.anamnesis, payload)
    }
  },
  actions: {
    login ({ commit, dispatch }, { login, password }) {
      return new Promise((resolve, reject) => {
        axios.post(`${api}/authpatient/`, { login, password }, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then((response) => {
            if (!response.data.id) {
              reject(new Error('Пользователь не зарегистрирован'))
            } else {
              commit.setSessionId(response.data)
              dispatch.getUserData(response.data)
              dispatch.getUserAnamnesis(response.data)
              resolve(response.data)
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },

    getUserData ({ commit }, data) {
      return new Promise((resolve) => {
        axios.post(`${api}/patientgetpatientinfo/`, data)
          .then((response) => {
            commit.setUserData(response.data)
            resolve(response.data)
          })
      })
    },

    getUserAnamnesis ({ commit }, data) {
      return new Promise((resolve) => {
        axios.post(`${api}/patientgetpatientanamnesis/`, data)
          .then((response) => {
            commit.setUserAnamnesis(response.data)
            resolve(response.data)
          })
      })
    },

    setUserAnamnesis ({ state }) {
      return new Promise((resolve) => {
        axios.post(`${api}/patientaddpatientanamnesis//`, { session_id: state.session_id, patient_id: state.user.id, ...state.anamnesis })
          .then((response) => {
            // commit.setUserAnamnesis(response.data);
            resolve(response.data)
          })
      })
    }
  },
  modules: {
  }
})
