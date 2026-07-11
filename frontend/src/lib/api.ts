import axios from 'axios';
import type {
  AttackDetail,
  AttackGenerateResponse,
  AttackListItem,
  DetectionRule,
  GenerateAttackRequest,
  IOC,
  IncidentReport,
  ReportListItem,
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 120_000, // scenario generation can take a while - LLM round trips
});

// Surface a readable message regardless of what the backend/network throws
apiClient.interceptors.response.use(
  (res) => res,
  (error) => {
    const detail =
      error?.response?.data?.detail ||
      error?.message ||
      'Something went wrong talking to the backend.';
    return Promise.reject(new Error(detail));
  }
);

export const api = {
  health: () => apiClient.get('/api/health').then((r) => r.data),

  generateAttack: (payload: GenerateAttackRequest) =>
    apiClient
      .post<AttackGenerateResponse>('/api/attacks/generate', payload)
      .then((r) => r.data),

  listAttacks: (skip = 0, limit = 20) =>
    apiClient
      .get<AttackListItem[]>('/api/attacks/', { params: { skip, limit } })
      .then((r) => r.data),

  getAttack: (id: string) =>
    apiClient.get<AttackDetail>(`/api/attacks/${id}`).then((r) => r.data),

  generateIOCs: (attackId: string) =>
    apiClient.post<IOC[]>(`/api/attacks/${attackId}/iocs/generate`).then((r) => r.data),

  listIOCs: (attackId: string) =>
    apiClient.get<IOC[]>(`/api/attacks/${attackId}/iocs`).then((r) => r.data),

  generateDetections: (attackId: string, ruleFormat: 'sigma' | 'yara', maxStages = 5) =>
    apiClient
      .post<DetectionRule[]>(`/api/attacks/${attackId}/detections/generate`, {
        rule_format: ruleFormat,
        max_stages: maxStages,
      })
      .then((r) => r.data),

  listDetections: (attackId: string) =>
    apiClient.get<DetectionRule[]>(`/api/attacks/${attackId}/detections`).then((r) => r.data),

  generateReport: (attackId: string) =>
    apiClient.post<IncidentReport>(`/api/attacks/${attackId}/reports/generate`).then((r) => r.data),

  listReports: (attackId: string) =>
    apiClient.get<ReportListItem[]>(`/api/attacks/${attackId}/reports`).then((r) => r.data),

  getReport: (attackId: string, reportId: string) =>
    apiClient
      .get<IncidentReport>(`/api/attacks/${attackId}/reports/${reportId}`)
      .then((r) => r.data),
};
