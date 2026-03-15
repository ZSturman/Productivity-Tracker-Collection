//
//  AddListView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import SwiftUI

struct AddListView: View {
    @EnvironmentObject var listViewModel: ListsViewModel
    @State var newListName: String = ""

    
    var body: some View {
        VStack(spacing: 20) {
            TextField("Add new list here...", text: $newListName)
                .font(.headline)
                .padding(.leading)
                .frame(height: 55)
                .background(Color(.secondarySystemFill))
                .cornerRadius(10)
                .padding(.horizontal)
            
            Button(action: {
                listViewModel.addList(listName: newListName)
                newListName = ""
            }, label: {
                Text("Add List")
                    .font(.headline)
                    .padding(.leading)
                    .frame(height: 55)
                    .cornerRadius(10)
                    .padding(.horizontal)
            })
            .padding(.horizontal)
            
            List {
                ForEach(listViewModel.lists, id: \.self) { list in
                    Text(list.name ?? "")
                }
            }
            .listStyle(PlainListStyle())
        }
        .navigationTitle("Add List")
    }
}

struct AddListView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            AddListView()
                .environmentObject(ListsViewModel(container: DataController().container))
        }
    }
}
