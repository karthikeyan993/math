import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import './custom.css'
import Predict from '../../components/Predict.vue'
import Recall from '../../components/Recall.vue'
import DominoChain from '../../components/DominoChain.vue'
import StaircaseSum from '../../components/StaircaseSum.vue'
import OddSquares from '../../components/OddSquares.vue'
import TrominoTiling from '../../components/TrominoTiling.vue'
import FocusTimer from '../../components/FocusTimer.vue'
import Checkpoint from '../../components/Checkpoint.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Predict', Predict)
    app.component('Recall', Recall)
    app.component('DominoChain', DominoChain)
    app.component('StaircaseSum', StaircaseSum)
    app.component('OddSquares', OddSquares)
    app.component('TrominoTiling', TrominoTiling)
    app.component('FocusTimer', FocusTimer)
    app.component('Checkpoint', Checkpoint)
  },
} satisfies Theme
