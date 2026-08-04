import { createApp } from 'vue'
import {
  Alert,
  Breadcrumb,
  Button,
  Card,
  Checkbox,
  Col,
  Descriptions,
  Empty,
  Form,
  Input,
  Layout,
  List,
  Modal,
  Radio,
  Result,
  Row,
  Select,
  Space,
  Spin,
  Switch,
  Table,
  Tabs,
  Tag,
  Tooltip,
  Upload,
} from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import App from './App.vue'
import router from './router'
import './styles/global.css'

const app = createApp(App)
for (const component of [
  Alert, Breadcrumb, Button, Card, Checkbox, Col, Descriptions, Empty, Form,
  Input, Layout, List, Modal, Radio, Result, Row, Select, Space, Spin, Switch,
  Table, Tabs, Tag, Tooltip, Upload,
]) {
  app.use(component)
}
app.use(router).mount('#app')
