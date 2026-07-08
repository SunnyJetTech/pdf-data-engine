"use client"

import { useEffect, useState } from "react"

import {
  getUsers,
  deleteUser,
} from "@/api/admin.api"

export default function UsersPage() {
  const [users, setUsers] =
    useState<any[]>([])

  useEffect(() => {
    loadUsers()
  }, [])

  async function loadUsers() {
    const response =
      await getUsers()

    setUsers(response.data ?? [])
  }

  async function handleDelete(id: number) {
    if (
      !confirm(
        "Delete this user permanently?"
      )
    )
      return

    await deleteUser(id)

    loadUsers()
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Users
      </h1>

      <table className="w-full border">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.full_name}</td>

              <td>{user.email}</td>

              <td>
                <button
                  onClick={() =>
                    handleDelete(user.id)
                  }
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}