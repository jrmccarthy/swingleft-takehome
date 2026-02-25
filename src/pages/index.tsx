import Head from "next/head";
import Image from "next/image";
import { Geist, Geist_Mono } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { useState, useEffect } from 'react'
import { Box, Button, Field, Flex, Heading, Input, NativeSelect, Table } from "@chakra-ui/react"
import { FaSort, FaSortAlphaDown, FaSortAlphaDownAlt } from "react-icons/fa";
import { format } from 'date-fns'

const API_PATH = "http://172.233.223.212:3000/api"

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
  gte = "Greater than or equal to"
}

enum SortOrder {
  asc = "asc",
  desc = "desc",
}

interface IVoterRegDataItem {
  state: string
  deadline_in_person: string | null
  deadline_by_mail: string | null
  deadline_online: string | null
  election_day_registration: string
  online_registration_link: string
  description: string
}

export default function Home() {
  const [voterRegData, setVoterRegData] = useState<[IVoterRegDataItem] | []>([])
  const [filter_by, set_filter_by] = useState<string>("state")
  const [filter_op, set_filter_op] = useState<string>("eq")
  const [filter_value, set_filter_value] = useState<string>("")
  const [order_by, set_order_by] = useState<string>("state")
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
    console.log("Filter by:" + filter_by)

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
    <div>
      <div>
        <Heading>Voter Registration Deadlines</Heading>
      </div>
      <br />
      <div>
        <SearchBox voterRegData={voterRegData} filter_by={filter_by} set_filter_by={set_filter_by} filter_op={filter_op} set_filter_op={set_filter_op} filter_value={filter_value} set_filter_value={set_filter_value} order_by={order_by} sort_order={sort_order} />
      </div>
      <br />
      <div>
        <VoterRegTable voterRegData={voterRegData} order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
      </div>
    </div>
  )
}

function SearchBox({voterRegData, filter_by, set_filter_by, filter_op, set_filter_op, filter_value, set_filter_value, order_by, sort_order}) {
  const [filter_by_select, set_filter_by_select] = useState<string>(filter_by)
  const [filter_op_select, set_filter_op_select] = useState<string>(filter_op)
  const [filter_value_input, set_filter_value_input] = useState<string>(filter_value)
  
  function setSearchTerms(e) {
    e.preventDefault()
    set_filter_by(filter_by_select)
    set_filter_op(filter_op_select)
    set_filter_value(filter_value_input)
  }
  function resetSearchTerms() {
    set_filter_by("state")
    set_filter_op("eq")
    set_filter_value("")
    set_filter_by_select("state")
    set_filter_op_select("eq")
    set_filter_value_input("")
  }

  return (
    <form>
      <Flex align="center" gap="3">
        <Box>
          <NativeSelect.Root id="filter_by">
            <NativeSelect.Field value={filter_by_select} onChange={(e) => set_filter_by_select(e.target.value)}>
              <option value="state">State</option>
              <option value="deadline_in_person">Registration Deadline In-Person</option>
              <option value="deadline_by_mail">Registration Deadline By Mail</option>
              <option value="deadline_online">Registration Deadline Online</option>
              <option value="election_day_registration">Election Day Registration</option>
              <option value="online_registration_link">Online Registration Link</option>
            </NativeSelect.Field>
          </NativeSelect.Root>
        </Box>
        <Box>
          <NativeSelect.Root id="filter_op">
            <NativeSelect.Field value={filter_op_select} onChange={(e) => set_filter_op_select(e.target.value)}>
            {/* <NativeSelect.Field value={filter_op} onChange={(e) => console.log("filter op " + e.target.value)}> */}
              {Object.keys(FilterOp).map((item) => (
                <option value={item}>{FilterOp[item]}</option>
              ))}
            </NativeSelect.Field>
          </NativeSelect.Root>
        </Box>
        <Box>
          <Field.Root id="filter_value">
            <Field.Label></Field.Label>
            <Input placeholder="Filter value..." value={filter_value_input} onChange={(e) => set_filter_value_input(e.target.value)}/>
          </Field.Root>
        </Box>
        <Box>
          <Button size="sm" mt="4" type="submit" onClick={setSearchTerms}>
            Apply
          </Button>
        </Box>
        <Box>
          <Button size="sm" mt="4" onClick={resetSearchTerms}>
            Reset
          </Button>
        </Box>
      </Flex>
    </form>
  )
}

function SortIconContainer({col_name, order_by, sort_order}) {
  if (col_name === order_by) {
    if (sort_order === "asc") {
// @ts-ignore : Typescript really doesn't like these Icons even though they are fine
      return (<div><FaSortAlphaDown /></div>)
    } else {
// @ts-ignore : Typescript really doesn't like these Icons even though they are fine
      return (<div><FaSortAlphaDownAlt /></div>)
    }
  } else {
// @ts-ignore : Typescript really doesn't like these Icons even though they are fine
    return (<div><FaSort /></div>)
  }
}

function TableHeaderWithSort({display_value, col_name, order_by, sort_order, set_order_by, set_sort_order}) {
  function clickHandler({col_name, order_by, sort_order}) {
    if (order_by === col_name) {
      if (sort_order === "asc") {
        set_sort_order("desc")
      } else {
        set_sort_order("asc")
      }
    } else {
      set_sort_order("asc")
    }
    set_order_by(col_name)
  }
  
  return (
    <Table.ColumnHeader onClick={(e) => clickHandler({col_name, order_by, sort_order})}>
      <Flex gap="1" align="center">
        {display_value}
        <Box>
          <SortIconContainer col_name={col_name} order_by={order_by} sort_order={sort_order} />
        </Box>
      </Flex>
    </Table.ColumnHeader>
  )
}

function VoterRegTable({voterRegData, order_by, sort_order, set_order_by, set_sort_order}) {
  console.log("voter data: ")
  console.log(voterRegData)

  return (
    <Table.Root>
      <Table.Caption />
      <Table.Header>
        <Table.Row>
          {/* <Table.ColumnHeader>State</Table.ColumnHeader> */}
          <TableHeaderWithSort display_value="State" col_name="state"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          <TableHeaderWithSort display_value="Registration Deadline In-Person" col_name="deadline_in_person"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          <TableHeaderWithSort display_value="Registration Deadline By Mail" col_name="deadline_by_mail"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          <TableHeaderWithSort display_value="Registration Deadline Online" col_name="deadline_online"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          <TableHeaderWithSort display_value="Election Day Registration" col_name="election_day_registration"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          <TableHeaderWithSort display_value="Online Registration Link" col_name="online_registration_link"  order_by={order_by} sort_order={sort_order} set_order_by={set_order_by} set_sort_order={set_sort_order} />
          {/* <Table.ColumnHeader>Registration Deadline In-Person </Table.ColumnHeader>
          <Table.ColumnHeader>Registration Deadline By Mail	</Table.ColumnHeader>
          <Table.ColumnHeader>Registration Deadline Online	</Table.ColumnHeader>
          <Table.ColumnHeader>Election Day Registration</Table.ColumnHeader>
          <Table.ColumnHeader>Online Registration Link</Table.ColumnHeader> */}
          <Table.ColumnHeader>Description</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {voterRegData.map((item: IVoterRegDataItem) => (
          <Table.Row key={item.state}>
            <Table.Cell>{item.state}</Table.Cell>
            <Table.Cell>{item.deadline_in_person}
            </Table.Cell>
            <Table.Cell>{item.deadline_by_mail}
            </Table.Cell>
            <Table.Cell>{item.deadline_online}
            </Table.Cell>
            <Table.Cell>{item.election_day_registration}</Table.Cell>
            <Table.Cell>{item.online_registration_link}</Table.Cell>
            <Table.Cell>{item.description}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}


