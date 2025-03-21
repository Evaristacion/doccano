import { PerspectiveDTO } from '@/services/application/perspective/perspectiveData'
import { PerspectiveRepository } from '@/domain/models/perspective/perspectiveRepository'
import { perspectiveItem } from '@/domain/models/perspective/perspective'
import ApiService from '@/services/api.service'

function toModel(dto: PerspectiveDTO): perspectiveItem {
  return {
    id: dto.id,
    name: dto.name,
    type: String(dto.type),
    project_id: dto.project
  }
}

export class ApiPerspectiveRepository implements PerspectiveRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: string): Promise<perspectiveItem[]> {
    const url = `/projects/${projectId}/perspectives`
    const response = await this.request.get(url)
    return response.data.results.map((item: any) => toModel(item))
  }

  async create(projectId: string | number, data: perspectiveItem): Promise<perspectiveItem> {
    const url = `/projects/${projectId}/perspectives`
    const response = await this.request.post(url, data)
    return toModel(response.data)
  }

  async update(projectId: string | number, perspectiveId: number, 
    data: perspectiveItem): Promise<perspectiveItem> {
    const url = `/projects/${projectId}/perspectives/${perspectiveId}`
    const response = await this.request.put(url, data)
    return toModel(response.data)
  }

  async delete(projectId: string | number, perspectiveId: number): Promise<void> {
    const url = `/projects/${projectId}/perspectives/${perspectiveId}`
    await this.request.delete(url)
  }
}