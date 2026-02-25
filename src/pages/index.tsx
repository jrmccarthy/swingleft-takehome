import Head from "next/head";
import Image from "next/image";
import { Geist, Geist_Mono } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { useState, useEffect } from 'react'
import { For, Stack, Table } from "@chakra-ui/react"
import { format } from 'date-fns'

const API_PATH = "http://127.0.0.1:5328/api"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

enum FilterOp {
  eq = "Equals",
  neq = "Not Equals",
  lt = "Less than",
  lte = "Less than or equal to",
  gt = "Greater than",
  gte = "Greater than or equal to",
  none = ""
}

enum SortOrder {
  asc = "Ascending",
  desc = "Descending",
}

interface IVoterRegDataItem {
  state: string
  deadline_by_mail: Date | null
  deadline_in_person: Date | null
  deadline_online: Date | null
  election_day_registration: string
  online_registration_link: string
  description: string
}

export default function Home() {
  const [voterRegData, setVoterRegData] = useState<[IVoterRegDataItem] | []>([])
  const [filter_by, set_filter_by] = useState<string>("")
  const [filter_op, set_filter_op] = useState<FilterOp>(FilterOp.none)
  const [filter_value, set_filter_value] = useState<string>("")
  const [order_by, set_order_by] = useState<string>("")
  const [sort_order, set_sort_order] = useState<SortOrder>(SortOrder.asc)

  useEffect(() => {
    const params = new URLSearchParams({
      filter_by: filter_by,
      filter_op: filter_op,
      filter_value: filter_value,
      order_by: order_by,
      sort_order: sort_order
    })

    const path = `${API_PATH}/voter_reg_deadline?${params}`

    fetch(
      path
    ).then(response => {
      console.log(response)
      return response.json()
    }).then(data => {
      setVoterRegData(data)
    }).catch(e => {
      console.error(e)
    })
  }, [filter_by, filter_op, filter_value, order_by, sort_order])

  return (
    <Table.Root>
      <Table.Caption />
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader>State</Table.ColumnHeader>
          <Table.ColumnHeader>Registration Deadline In-Person</Table.ColumnHeader>
          <Table.ColumnHeader>Registration Deadline By Mail	</Table.ColumnHeader>
          <Table.ColumnHeader>Registration Deadline Online	</Table.ColumnHeader>
          <Table.ColumnHeader>Election Day Registration</Table.ColumnHeader>
          <Table.ColumnHeader>Online Registration Link</Table.ColumnHeader>
          <Table.ColumnHeader>Description</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {voterRegData.map((item: IVoterRegDataItem) => (
          <Table.Row key={item.state}>
            <Table.Cell>{item.state}</Table.Cell>
            <Table.Cell>{item.deadline_by_mail 
              ? format(item.deadline_by_mail, "YYYY-MM-DD")
              : ""
            }</Table.Cell>
            <Table.Cell>{item.deadline_in_person 
              ? format(item.deadline_in_person, "YYYY-MM-DD")
              : ""}</Table.Cell>
            <Table.Cell>{item.deadline_online 
              ? format(item.deadline_online, "YYYY-MM-DD")
              : ""}</Table.Cell>
            <Table.Cell>{item.election_day_registration}</Table.Cell>
            <Table.Cell>{item.online_registration_link}</Table.Cell>
            <Table.Cell>{item.description}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}
